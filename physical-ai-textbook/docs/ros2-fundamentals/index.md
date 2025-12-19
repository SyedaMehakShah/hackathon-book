# ROS 2 Fundamentals

## Introduction to ROS 2

Robot Operating System 2 (ROS 2) is not an operating system but rather a flexible framework for writing robot software. It provides services such as hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more. ROS 2 is designed to be suitable for real-world robotics applications, including those requiring safety and security.

## Architecture of ROS 2

### DDS-Based Communication

Unlike ROS 1, which used a centralized master architecture, ROS 2 is built on Data Distribution Service (DDS), a middleware standard for real-time and distributed systems. This provides:

- Peer-to-peer communication
- Improved reliability and fault tolerance
- Better support for multi-robot systems
- Enhanced security capabilities

### Nodes and Processes

In ROS 2, a node is a process that performs computation. Nodes are written using client libraries such as `rclcpp` for C++ or `rclpy` for Python. A single process can contain multiple nodes.

### Topics and Publishers/Subscribers

Topics are named buses over which nodes exchange messages. A node can publish messages to a topic or subscribe to messages from a topic. This creates a many-to-many relationship between publishers and subscribers.

### Services and Actions

Services provide a request/response communication pattern between nodes. A service client sends a request to a service server, which returns a response.

Actions are similar to services but are designed for long-running tasks. They provide feedback during execution and can be preempted.

## Setting Up a ROS 2 Workspace

### Installation

ROS 2 can be installed on various platforms. The installation process involves:

1. Setting up the environment
2. Installing ROS 2 packages
3. Configuring the development environment

### Creating a Workspace

ROS 2 uses colcon for building packages. A typical workspace structure includes:

```bash
ros2_workspace/
├── src/
│   ├── package1/
│   ├── package2/
│   └── ...
```

## Core Concepts

### Packages

A ROS 2 package contains nodes, libraries, and other assets necessary for robot functionality. Key components include:

- `package.xml`: Manifest file containing package metadata
- `CMakeLists.txt`: Build configuration file for C++
- `setup.py`: Build configuration file for Python

### Messages

Messages are the data structures used for communication between nodes. They are defined in `.msg` files and can contain primitive data types and other message types.

### Parameters

Parameters are configuration values that can be set at runtime. They allow for dynamic reconfiguration of nodes without recompilation.

## ROS 2 for Humanoid Robotics

### Key Packages

Several ROS 2 packages are particularly important for humanoid robots:

- `ros2_controllers`: Real-time control framework
- `moveit2`: Motion planning framework
- `navigation2`: Navigation stack
- `rviz2`: Visualization tool
- `ros_gz`: Integration with Gazebo simulation

### Control Architecture

Humanoid robots typically use a hierarchical control architecture:

1. **High-level planning**: Path planning, motion planning
2. **Mid-level control**: Balance control, trajectory generation
3. **Low-level control**: Joint-level control, motor commands

## Practical Example: Creating a Simple Node

Here's a basic example of a ROS 2 node in Python:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Simulation Integration

ROS 2 provides excellent support for simulation environments, particularly through the `ros_gz` package which integrates with Gazebo. This allows for:

- Physics simulation
- Sensor simulation
- Realistic environment modeling
- Rapid testing of algorithms

## Best Practices

### Design Patterns

- Use composition over inheritance
- Separate concerns between nodes
- Use services for state queries, topics for streaming data
- Implement proper error handling and logging

### Performance

- Minimize message size
- Use appropriate QoS policies for different data types
- Profile your nodes for computational bottlenecks
- Consider threading for I/O operations

### Safety

- Implement proper node lifecycle management
- Use namespaces to avoid naming conflicts
- Validate incoming data
- Implement timeouts for critical operations

## Advanced Topics

### ROS 2 Middleware

ROS 2 supports different DDS implementations through a plugin architecture. This allows you to choose the most appropriate one for your application:

- **Fast DDS**: Performance-oriented
- **Cyclone DDS**: Memory-efficient
- **OpenSplice DDS**: Enterprise-grade

### Multi-Robot Systems

ROS 2 has built-in support for multi-robot systems through:

- Namespacing
- Discovery protocols
- Secure communication

## Conclusion

ROS 2 provides a robust and flexible framework for developing complex robotic systems, particularly well-suited for humanoid robotics applications. Its modern architecture addresses many limitations of ROS 1 while maintaining the core concepts that make ROS a powerful platform for robotics development.

Understanding ROS 2 fundamentals is crucial for anyone working in humanoid robotics, as it provides the foundation for communication between the various components of a robotic system.