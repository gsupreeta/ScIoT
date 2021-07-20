(define (domain MaintainTemperature)
    (:requirements
      :strips
      :typing
      :negative-preconditions
      :equality
    )

    (:predicates
      (sensor_input ?s)
      (user_input ?u)
      (temp ?t)
      (fan ?f)
      (sensor_input_humid ?h)
      (user_input_humid ?i)
    )

    (:action temperature-same
      :parameters (?s ?u ?t ?i ?h)
      :precondition (and (user_input ?u) (user_input_humid ?i) (sensor_input ?s) (sensor_input_humid ?h) (temp ?t))
      :effect (not(temp ?t))
    )
        
    (:action temp-different-user-input
      :parameters (?s ?u ?f ?h ?i)
      :precondition (and (user_input ?u) (user_input_humid ?i) (sensor_input ?s) (sensor_input_humid ?h) (fan ?f))
      :effect (not(fan ?f))
    )
    
    (:action temp-different-sensor-input
      :parameters (?s ?u ?f ?h ?i)
      :precondition (and (user_input ?u) (user_input_humid ?i) (sensor_input ?s) (sensor_input_humid ?h) (not(fan ?f)))
      :effect (fan ?f)
    )

)
