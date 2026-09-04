cat << 'EOF' > student_agent/solver.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# ==========================================
# Required Simulator Constraints (Must equal 30)
# ==========================================
TOP_SPEED = 8
ACCELARATION = 7
TURN_SPEED = 5
SENSOR_RANGE = 10

class StudentSolver(Node):
    def __init__(self):
        super().__init__('student_solver')
        self.scan_sub = self.create_subscription(LaserScan, '/mouse/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/mouse/cmd_vel', 10)
    
    def scan_callback(self, msg):
        cmd = Twist()
        d_left  = msg.ranges[0]
        d_front = msg.ranges[1]
        d_right = msg.ranges[2]  

        # Target distance to maintain from the right wall
        target_dist = 0.5

        # Basic Right-Wall Following Decision Tree
        if d_front < 0.6:
            # Dead end or wall ahead: Pivot left in place
            cmd.linear.x = 0.0
            cmd.angular.z = 1.0
        elif d_right > target_dist + 0.3:
            # Large gap on the right (corner): Turn right to follow it
            cmd.linear.x = 0.3 
            cmd.angular.z = -1.0
        elif d_right < target_dist - 0.2:
            # Drifting too close to the right wall: Veer left slightly
            cmd.linear.x = 0.4
            cmd.angular.z = 0.5
        else:
            # Path is clear and distance is optimal: Drive straight
            cmd.linear.x = 0.8
            cmd.angular.z = 0.0
        
        self.cmd_pub.publish(cmd)
    
def main(args=None):    
    rclpy.init(args=args)
    node = StudentSolver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
if __name__ == '__main__':
    main()
EOF
