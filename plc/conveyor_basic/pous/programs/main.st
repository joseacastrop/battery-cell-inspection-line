PROGRAM main
  VAR
    start_pb : BOOL AT %IX0.0;
    stop_pb : BOOL AT %IX0.1;
    motor_run : BOOL AT %QX0.0;
  END_VAR

motor_run := (start_pb OR motor_run) AND NOT stop_pb;

END_PROGRAM