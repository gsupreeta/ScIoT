(define (problem TemperatureControl)
(:domain MaintainTemperature)
 (:objects fan1 User1 Sensor1 Human1)
 (:init (fan fan1) (user_input User1) (sensor_input Sensor1) (human Human1))
 (:goal (and (not(fan fan1)) (user_input User1) (sensor_input Sensor1) (human Human1)))
)






