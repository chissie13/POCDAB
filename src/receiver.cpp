#include "tun_device.h"
#include <dab/packet/packet_parser.h>
#include <dab/msc_data_group/msc_data_group_parser.h>
#include <dab/ensemble/ensemble.h>
#include <dab/ensemble/service.h>
#include <dab/ensemble/service_component.h>
#include <dab/demodulator.h>
#include <dab/device/device.h>
#include <dab/device/rtl_device.h>
#include <dab/types/common_types.h>
#include <dab/types/gain.h>

#include <asio/io_service.hpp>
#include <asio/signal_set.hpp>

#include <cstdint>
#include <future>
#include <iostream>
#include <string>

int main(int argc, char **argv)
  {
   using namespace dab::literals;

//ensemblename tied to the frequency
  std::map<std::string,dab::frequency> mapOfMarks = {
    {"5A", 174928_kHz},{"5B", 176640_kHz},{"5C", 178352_kHz},{"5D", 180064_kHz},
    {"6A", 181936_kHz},{"6B", 183648_kHz},{"6C", 185360_kHz},{"6D", 187072_kHz},
    {"7A", 188928_kHz},{"7B", 190640_kHz},{"7C", 192352_kHz},{"7D", 194064_kHz},
    {"8A", 195936_kHz},{"8B", 197648_kHz},{"8C", 199360_kHz},{"8D", 201072_kHz},
    {"9A", 202928_kHz},{"9B", 204640_kHz},{"9C", 206352_kHz},{"9D", 208064_kHz},
    {"10A",209936_kHz},{"10B", 211648_kHz},{"10C", 213360_kHz},{"10D", 215072_kHz},
    {"11A", 216928_kHz},{"11B", 218640_kHz},{"11C", 220352_kHz},{"11D", 222064_kHz},
    {"12A", 223936_kHz},{"12B", 225648_kHz},{"12C", 227360_kHz},{"12D", 229072_kHz},
    {"13A", 230784_kHz},{"13B", 232496_kHz},{"13C", 234208_kHz},{"13D", 235776_kHz},
    {"13E", 237488_kHz},{"13F", 239200_kHz}
  };

  if(argc != 4)
    {
    std::cerr << "Correct usage: <data_over_dab> <destination_ip> <packet_address> <ensemble (5A, 9B, 12C etc.)>\n";
    return 1;
    }

  // Prepare our data queues for acquisition and demodulation
  dab::sample_queue_t samples{};
  dab::symbol_queue_t symbols{};

  // Prepare the input device
  dab::rtl_device device{samples};

  // device.enable(dab::device::option::automatic_gain_control);
  device.tune(mapOfMarks.find(argv[3]) -> second);
  device.gain(40_dB);

  // Start sample acquisition
  auto deviceRunner = std::async(std::launch::async, [&]{ device.run(); });

  // Initialize the demodulator
  dab::demodulator demod{samples, symbols, dab::kTransmissionMode1};
  auto demodRunner = std::async(std::launch::async, [&]{ demod.run(); });

  // Create an io_service for our virtual network device
  asio::io_service eventLoop{};

  // We need a dummy load or else the io_service run() function return immediately
  asio::io_service::work dummyLoad{eventLoop};
  auto tunRunner = std::async(std::launch::async, [&]{ eventLoop.run(); });

  // Create our virtual network device
  tunnel_for_device tunnel{eventLoop, "dabdata"};
  auto destination = std::string{argv[1]};
  tunnel.address(destination);
  auto error = tunnel.up();
  if(error)
    {
    throw error.message();
    }

  auto && signals = asio::signal_set{eventLoop, SIGINT};
  signals.async_wait([&](asio::error_code const err, int const){
    if(!err)
      {
      device.stop();
      demod.stop();
      eventLoop.stop();
      std::cout << "Received SIGNINT. Stopping\n";
      }
  });

  // Initialize the decoder
  auto ensemble = dab::ensemble{symbols, dab::kTransmissionMode1};

  // Prepare our packet parser
  auto packetParser = dab::packet_parser{std::uint16_t(std::stoi(argv[2]))};
  auto amountofemptypackets = 0;
  // Get the ensemble ready
  while(!ensemble && ensemble.update());

  // Check if we were able to succcessfully prepare the ensemble
  if(!ensemble)
    {
    return 1;
    }
  // Activate our service
  bool activated{};
  if(!activated)
    {
    for(auto const & service : ensemble.services())
      {
      // Check for a data service with a valid primary service component
      if(service.second->type() == dab::service_type::data && service.second->primary())
        {
        // Check if the primary service component claims to carry IPDT
        if(service.second->primary()->type() == 59)
          {
          // Register our "data received" callback with the service
          ensemble.activate(service.second, [&](std::vector<std::uint8_t> data){
            // Parse the received data
            auto parseResult = packetParser.parse(data);
            if(parseResult.first == dab::parse_status::ok)
              {
              // Parse the received data back into an MSC data group
              auto datagroupParser = dab::msc_data_group_parser{};
              parseResult = datagroupParser.parse(parseResult.second);

              if(parseResult.first == dab::parse_status::ok)
                {
                // Enqueue the data to be sent to the operating system
                tunnel.enqueue(std::move(parseResult.second));
                }
              else
                {
                std::cout << "datagroupError: " << std::uint32_t(parseResult.first) << '\n';
                }
              }
            else if(parseResult.first != dab::parse_status::incomplete)
              {
		auto packetError = std::uint32_t(parseResult.first);
		if(packetError == 1){
			amountofemptypackets = amountofemptypackets + 1;
			std::cout << "packet received, but there was no data in it: " << amountofemptypackets << '\n';
		}
		else{
              std::cout << "packetError: " << std::uint32_t(parseResult.first) << '\n';
              std::cout << std::endl;
		}
              }
            });
          activated = true;
          }
        }
      }
    }
  while(!eventLoop.stopped() && ensemble.update())
    {
  
    }
  }

