import React, { useState, useEffect } from 'react';

const WeekTracker = () => {
  const [progress, setProgress] = useState({});
  const [activeWeek, setActiveWeek] = useState(1);

  // Load progress from localStorage
  useEffect(() => {
    const savedProgress = localStorage.getItem('courseProgress');
    if (savedProgress) {
      setProgress(JSON.parse(savedProgress));
    }
  }, []);

  // Save progress to localStorage
  useEffect(() => {
    localStorage.setItem('courseProgress', JSON.stringify(progress));
  }, [progress]);

  // 13-week curriculum structure
  const weeks = [
    { id: 1, title: "Foundations", topics: ["Introduction", "Embodied Intelligence"] },
    { id: 2, title: "Foundations", topics: ["Embodied Intelligence (cont.)", "Introduction to Physical AI"] },
    { id: 3, title: "ROS 2 Fundamentals", topics: ["ROS 2 Overview", "Nodes and Topics"] },
    { id: 4, title: "ROS 2 Fundamentals", topics: ["Services and Actions", "ROS 2 for Humanoid Robotics"] },
    { id: 5, title: "Simulation Environments", topics: ["Gazebo Introduction", "Gazebo Physics"] },
    { id: 6, title: "Simulation Environments", topics: ["Unity Integration", "Simulation for Humanoid Robotics"] },
    { id: 7, title: "NVIDIA Isaac", topics: ["Isaac Platform", "Isaac for Humanoid Robotics"] },
    { id: 8, title: "VLA Systems", topics: ["Vision-Language-Action Overview", "Multimodal Learning"] },
    { id: 9, title: "VLA Systems", topics: ["VLA Architectures", "Applications"] },
    { id: 10, title: "Conversational Robotics", topics: ["Conversational AI", "Dialogue Systems"] },
    { id: 11, title: "Conversational Robotics", topics: ["Human-Robot Interaction", "Social Robotics"] },
    { id: 12, title: "Capstone Project", topics: ["Project Planning", "System Architecture"] },
    { id: 13, title: "Capstone Project", topics: ["Implementation", "Testing and Evaluation"] }
  ];

  const toggleWeekCompletion = (weekId) => {
    const newProgress = { ...progress };
    newProgress[weekId] = !progress[weekId];
    setProgress(newProgress);
  };

  const completedWeeks = Object.keys(progress).filter(weekId => progress[weekId]).length;
  const completionPercentage = Math.round((completedWeeks / weeks.length) * 100);

  return (
    <div className="week-tracker-container">
      <div className="progress-summary">
        <h3>Course Progress</h3>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${completionPercentage}%` }}
          ></div>
        </div>
        <div className="progress-text">
          {completedWeeks} of {weeks.length} weeks completed ({completionPercentage}%)
        </div>
      </div>

      <div className="weeks-list">
        <h4>13-Week Curriculum</h4>
        {weeks.map(week => (
          <div 
            key={week.id} 
            className={`week-item ${progress[week.id] ? 'completed' : ''} ${activeWeek === week.id ? 'active' : ''}`}
            onClick={() => setActiveWeek(week.id)}
          >
            <div className="week-header">
              <span className="week-number">Week {week.id}</span>
              <span className="week-title">{week.title}</span>
              <button 
                className={`completion-toggle ${progress[week.id] ? 'completed' : ''}`}
                onClick={(e) => { e.stopPropagation(); toggleWeekCompletion(week.id); }}
                aria-label={progress[week.id] ? `Mark Week ${week.id} as incomplete` : `Mark Week ${week.id} as complete`}
              >
                {progress[week.id] ? '✓' : '○'}
              </button>
            </div>
            <div className="week-topics">
              {week.topics.map((topic, index) => (
                <div key={index} className="topic">
                  {topic}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeekTracker;