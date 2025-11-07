#!/usr/bin/env python3

import rclpy
from asl_tb3_lib.control import BaseController
from asl_tb3_msgs.msg import TurtleBotControl

class PerceptionController(BaseController):
    def __init__(self):
        super().__init__("perception_controller")
        self.declare_parameter("active", True)
        self.last_time = None

    @property
    def active(self) -> bool:
        return self.get_parameter("active").value
    
    def compute_control(self):
        control_msg = TurtleBotControl()
        control_msg.v = 0.0
        if self.active:
            control_msg.omega = 0.5
            self.last_time = None
        else:
            cur_time = self.get_clock().now().nanoseconds / 1e9

            if self.last_time is None:
                self.last_time = cur_time

            elapsed = cur_time - self.last_time

            if elapsed >= 5.0:
                self.set_parameters([rclpy.Parameter("active", value=True)])
                control_msg.omega = 0.5
            else:
                control_msg.omega = 0.0
        
        return control_msg
    
def main(args=None):
    rclpy.init(args=args)
    node = PerceptionController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()
    
    
