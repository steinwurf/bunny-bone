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
HX711 hx711;
const float scale = 603.851f;
const long offset = 8678;
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
const int sleep_interval_ms = SECONDS(15);

/// The number of readings to buffer before overwriting the oldest.
const int max_buffered_readings = 2000; // ~8 hours of buffer

uint32_t sequence_number = 0;
CircularBuffer<bunny_bone::reading, max_buffered_readings> buffered_readings;
uint8_t send_buffer[14];
bool connected = false;

void setup() {
  SimbleeBLE.deviceName = "Bunny_1";
  SimbleeBLE.advertisementData = "data";
  SimbleeBLE.advertisementInterval = MILLISECONDS(1500);
  SimbleeBLE.txPowerLevel = -8;  // (-20dbM to +4 dBm)
  SimbleeBLE.customUUID = "2220";
  SimbleeBLE.begin();


#ifdef HAS_HX711
  hx711.begin(2,3); // parameter "gain" is ommited; the default value 128 is used by the library
  hx711.set_scale(scale);
  hx711.set_offset(offset * hx711.get_scale());
#endif

#ifdef DEBUG
  Serial.begin(9600);
#endif
  DEBUG_PRINTLN("Started");
  DEBUG_PRINT("Buffer can store ");
  DEBUG_PRINT((max_buffered_readings * sleep_interval_ms) * 0.000000277778f);
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

  auto time_to_sleep_ms = sleep_interval_ms;
  auto before_ms = millis();

  // Always buffer readings
  buffered_readings.push(read_data());

  // Send as much as possible
  while(connected && !buffered_readings.isEmpty())
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
  auto time_spent = (millis() - before_ms);
  if (time_spent < time_to_sleep_ms)
  {
    Simblee_ULPDelay(time_to_sleep_ms - time_spent);
  }
}

bunny_bone::reading read_data()
{
#ifndef HAS_HX711
  int16_t result = (int16_t)Simblee_temperature(CELSIUS);
#endif
#ifdef HAS_HX711
  hx711.power_up();
  int16_t result = (int16_t)hx711.get_units(1);
  hx711.power_down();
#endif
  bunny_bone::reading reading = { millis(), result };
  DEBUG_PRINT("time: ");
  DEBUG_PRINT(reading.m_time);
  DEBUG_PRINT("ms - ");
  DEBUG_PRINTLN(reading.m_reading);
  return reading;
}

bool send(const bunny_bone::reading& reading)
{
  auto offset = 0;
  memcpy(send_buffer + offset, &reading.m_time, sizeof(bunny_bone::reading::m_time));
  offset += sizeof(bunny_bone::reading::m_time);
  memcpy(send_buffer + offset, &reading.m_reading, sizeof(bunny_bone::reading::m_reading));
  offset += sizeof(bunny_bone::reading::m_reading);
  uint32_t send_time = millis();
  memcpy(send_buffer + offset, &send_time, sizeof(send_time));
  offset += sizeof(send_time);
  memcpy(send_buffer + offset, &sequence_number, sizeof(sequence_number));
  auto result = SimbleeBLE.send((char*)send_buffer, sizeof(send_buffer));
  if (result)
  {
    sequence_number++;
  }
  return result;
}
