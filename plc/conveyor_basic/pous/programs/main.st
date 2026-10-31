PROGRAM main
  VAR
    start_pb        : BOOL AT %MX0.0;
    stop_pb         : BOOL AT %MX0.1;
    belt_moving     : BOOL AT %MX0.2;
    motor_run       : BOOL AT %QX0.0;
    start_beacon    : BOOL AT %QX0.1;
    start_requested : BOOL;
    belt_no_motion  : BOOL;
    startup_timer   : TON;
    confirm_timer   : TON;
  END_VAR

(* 1. Memory: remember that a start was requested *)
  start_requested := (start_pb OR start_requested) AND NOT stop_pb;

  (* 2. Start-up delay *)
  startup_timer(IN := start_requested, PT := T#3s);

  (* 3. Outputs *)
  start_beacon := start_requested AND NOT startup_timer.Q;
  motor_run    := startup_timer.Q;

  (* 4. Running confirmation *)
  confirm_timer(IN := motor_run AND NOT belt_moving, PT := T#2s);
  belt_no_motion := confirm_timer.Q;

END_PROGRAM