(define (problem TemperatureControl)
(:domain MaintainTemperature)
 (:objects fan1 User1 Sensor1 User_humid1 Sensor_humid1)
 (:init (fan fan1) (user_input User1) (sensor_input Sensor1) (user_input_humid User_humid1) (sensor_input_humid Sensor_humid1))
 (:goal (and (not(fan fan1)) (user_input User1) (sensor_input Sensor1)(user_input_humid User_humid1) (sensor_input_humid Sensor_humid1)))
)
