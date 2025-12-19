// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'intro',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Week 1-2: Foundations',
      items: [
        'embodied-intelligence/index',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Week 3-4: ROS 2 Fundamentals',
      items: [
        'ros2-fundamentals/index',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Week 5-6: Simulation Environments',
      items: [
        'gazebo-unity/index',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Week 7: NVIDIA Isaac',
      items: [
        'nvidia-isaac/index',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Week 8-9: Vision-Language-Action Systems',
      items: [
        'vla-systems/index',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Week 10-11: Conversational Robotics',
      items: [
        'conversational-robotics/index',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Week 12-13: Capstone Project',
      items: [
        'capstone-project/index',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Appendix',
      items: [
        'appendix/index',
      ],
      collapsed: true,
    },
  ],
};

export default sidebars;