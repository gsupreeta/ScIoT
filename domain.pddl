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
    )

    (:action temperature-same
      :parameters (?s ?u ?t)
      :precondition (and (user_input ?u) (sensor_input ?s) (temp ?t))
      :effect (not(temp ?t))
    )
        
    (:action temp-different-user-input
      :parameters (?s ?u ?f)
      :precondition (and (user_input ?u) (sensor_input ?s) (fan ?f))
      :effect (not(fan ?f))
    )
    
    (:action temp-different-sensor-input
      :parameters (?s ?u ?f)
      :precondition (and (user_input ?u) (sensor_input ?s) (not(fan ?f)))
      :effect (fan ?f)
    )

)