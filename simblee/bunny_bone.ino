#include <SimbleeBLE.h>
#include <CircularBuffer.h>
#include <array>

///////////////////////
///     DEFINES     ///
///////////////////////
/// Defines whether to use the internal temperature sensor or the HX711
#define HAS_HX711
/// Defines whether to enable debug (and serial communication or not)
// #define DEBUG

#ifdef HAS_HX711
#include "HX711.h"
HX711 scale;
#endif

#ifdef DEBUG
  #define DEBUG_PRINT(...) Serial.print(__VA_ARGS__)
  #define DEBUG_PRINTLN(...) Serial.println(__VA_ARGS__)
#else
  #define DEBUG_PRINT(...)
  #define DEBUG_PRINTLN(...)
#endif


namespace bunny_bone
{
/// class for containing the readings and their measurement time
/// (in milliseconds since boot).
struct reading
{
  uint32_t m_time;
  int16_t m_reading;
};
}

/// The time to sleep between each reading
const int sleep_interval = MILLISECONDS(15000);

/// The number of readings to buffer before overwriting the oldest.
const int max_buffered_readings = 2000; // ~8 hours of buffer

CircularBuffer<bunny_bone::reading, max_buffered_readings> buffered_readings;
uint8_t send_buffer[6];
bool connected = false;

void setup() {
  SimbleeBLE.deviceName = "Bunny_1";
  SimbleeBLE.advertisementData = "data";
  SimbleeBLE.advertisementInterval = MILLISECONDS(1500);
  SimbleeBLE.txPowerLevel = -12;  // (-20dbM to +4 dBm)
  SimbleeBLE.customUUID = "2220";
  SimbleeBLE.begin();


#ifdef HAS_HX711
  // Sleep for some time before calling tare.
  Simblee_ULPDelay(SECONDS(5));
  scale.begin(2,3);    // parameter "gain" is ommited; the default value 128 is used by the library
  scale.set_scale(603.851f);
  scale.tare();
#endif

#ifdef DEBUG
  Serial.begin(9600);
#endif
  DEBUG_PRINTLN("Started");
  DEBUG_PRINT("Buffer can store ");
  DEBUG_PRINT((max_buffered_readings * sleep_interval) * 0.000000277778f);
  DEBUG_PRINTLN(" Hours.");
}

void SimbleeBLE_onConnect(){
  DEBUG_PRINTLN("Connected");
  connected = true;
}

void SimbleeBLE_onDisconnect(){
  DEBUG_PRINTLN("Disconnected");
  connected = false;
}

void loop() {
  // Always buffer readings
  buffered_readings.push(read_data());
  if (connected)
  {
    // Send as much as possible
    while(!buffered_readings.isEmpty())
    {
      auto reading = buffered_readings.first();
      if (!send(reading))
      {
        DEBUG_PRINT(buffered_readings.size());
        DEBUG_PRINT(" readings still in buffer. But network is unavailable -");
        DEBUG_PRINTLN(" trying again later..");
        break;
      }
      /// If the reading was sent successfully - remove it from buffer
      buffered_readings.shift();
    }
  }

  Simblee_ULPDelay(sleep_interval);
}

bunny_bone::reading read_data()
{
#ifndef HAS_HX711
  int16_t result = (int16_t)Simblee_temperature(CELSIUS);
#endif
#ifdef HAS_HX711
  scale.power_up();
  scale.get_units(1);
  int16_t result = (int16_t)scale.get_units(1);

  scale.power_down();
#endif
  DEBUG_PRINTLN(result);
  return { millis(), result };
}

bool send(const bunny_bone::reading& reading)
{
  memcpy(send_buffer, &reading.m_time, sizeof(bunny_bone::reading::m_time));
  memcpy(send_buffer + sizeof(bunny_bone::reading::m_time), &reading.m_reading, sizeof(bunny_bone::reading::m_reading));
  return SimbleeBLE.send((char*)send_buffer, 6);
}
