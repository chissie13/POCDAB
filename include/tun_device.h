//this was not written by me, but was taken from www.github.com/Opendigitalradio/data-over-dab-example
#ifndef __DOD_TUN_DEVICE

#include <linux/if_tun.h>
#include <net/if.h>
#include <netinet/in.h>
#include <sys/ioctl.h>

#include <asio/io_service.hpp>
#include <asio/posix/stream_descriptor.hpp>

#include <array>
#include <functional>
#include <string>
#include <system_error>
#include <vector>

// A simple wrapper to handle tun device I/O using ASIO
struct tunnel_for_device
  {
  //Create a tun device wrapper with a user provided name
  tunnel_for_device(asio::io_service & eventLoop, std::string const & name);

  ~tunnel_for_device();

  // Enqueue data to be sent to the operating system
  void enqueue(std::vector<unsigned char> && data);
  
  // Put the interface up
  std::error_code up();

  // Retrieve the actual name of the tun device
  std::string const & name() const;

  // Get the device address
  std::string address();

  // Set the IPv4 address of the device.
  std::error_code address(std::string const & address);

  private:
    void do_write(std::vector<unsigned char> && data);

    std::error_code ioctl(int const type, ifreq & request);

    asio::posix::stream_descriptor m_device;

    std::string m_name{};
    int m_ioctlDummy{-1};
  };

#endif

