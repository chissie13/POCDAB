include("ExternalDependency")

set(${${PROJECT_NAME}_UPPER}_DEPS)

external_dependency(CMAKE
  NAME    "dabdemod"
  REPO    "https://github.com/Opendigitalradio/libdabdemod"
  )
external_dependency(CMAKE
  NAME    "dabdecode"
  REPO    "https://github.com/daanneek/dabdecode"
  )
external_dependency(CMAKE
  NAME    "dabdevice"
  REPO    "https://github.com/Opendigitalradio/libdabdevice"
  )
external_dependency(CMAKE
  NAME    "dabip"
  REPO    "https://github.com/Opendigitalradio/libdabip"
  )
