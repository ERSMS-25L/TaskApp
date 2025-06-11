import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import AuthGuard from './AuthGuard';

const Tasks = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ title: '', description: '', due_date: '' });

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_TASK_SERVICE_URL}/api/tasks/`);
      // Filter tasks for the current user only
      const userTasks = response.data.filter(task => task.user_id === user.backendId);
      setTasks(userTasks);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const createTask = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${process.env.REACT_APP_TASK_SERVICE_URL}/api/tasks/`, {
        title: form.title,
        description: form.description || undefined,
        due_date: form.due_date || undefined,
        user_id: user.backendId || 1 // Use Firebase user's backend ID
      });
      setForm({ title: '', description: '', due_date: '' });
      fetchTasks();
    } catch (err) {
      console.error('Error creating task:', err);
      setError(err);
    }
  };

  const markComplete = async (id) => {
    try {
      // Find the task to get its details for the notification
      const task = tasks.find(t => t.id === id);
      
      // Mark task as complete
      await axios.put(`${process.env.REACT_APP_TASK_SERVICE_URL}/api/tasks/${id}`, { completed: true });
      
      // Send notification email
      try {
        await axios.post(`${process.env.REACT_APP_NOTIFICATION_SERVICE_URL}/send-email-notification`, null, {
          params: {
            message: `Congratulations! You have completed the task: "${task.title}"`,
            subject: `Task Completed: ${task.title}`,
            recipient: user.email
          }
        });
        console.log('Completion notification sent successfully');
      } catch (notificationError) {
        console.error('Error sending completion notification:', notificationError);
        // Don't block the task completion if notification fails
      }
      
      fetchTasks();
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  const TaskContent = () => {
    if (loading) {
      return <div>Loading tasks...</div>;
    }

    if (error) {
      return <div>Error: {error.message}</div>;
    }

    return (
      <div>
        <h2>Task List</h2>
        <form onSubmit={createTask} style={{ marginBottom: '1rem' }}>
          <input 
            name="title" 
            placeholder="Title" 
            value={form.title} 
            onChange={handleChange} 
            required 
            style={{ marginRight: '0.5rem', padding: '0.5rem' }}
          />
          <input 
            name="description" 
            placeholder="Description" 
            value={form.description} 
            onChange={handleChange} 
            style={{ marginRight: '0.5rem', padding: '0.5rem' }}
          />
          <input 
            name="due_date" 
            placeholder="Due Date (YYYY-MM-DD)" 
            value={form.due_date} 
            onChange={handleChange} 
            style={{ marginRight: '0.5rem', padding: '0.5rem' }}
          />
          <button type="submit" style={{ padding: '0.5rem 1rem' }}>Add Task</button>
        </form>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5' }}>
              <th style={{ border: '1px solid #ddd', padding: '0.5rem' }}>ID</th>
              <th style={{ border: '1px solid #ddd', padding: '0.5rem' }}>Title</th>
              <th style={{ border: '1px solid #ddd', padding: '0.5rem' }}>Description</th>
              <th style={{ border: '1px solid #ddd', padding: '0.5rem' }}>Due Date</th>
              <th style={{ border: '1px solid #ddd', padding: '0.5rem' }}>Completed</th>
              <th style={{ border: '1px solid #ddd', padding: '0.5rem' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map(task => (
              <tr key={task.id}>
                <td style={{ border: '1px solid #ddd', padding: '0.5rem' }}>{task.id}</td>
                <td style={{ border: '1px solid #ddd', padding: '0.5rem' }}>{task.title}</td>
                <td style={{ border: '1px solid #ddd', padding: '0.5rem' }}>{task.description}</td>
                <td style={{ border: '1px solid #ddd', padding: '0.5rem' }}>{task.due_date ? task.due_date : '-'}</td>
                <td style={{ border: '1px solid #ddd', padding: '0.5rem' }}>{task.completed ? 'Yes' : 'No'}</td>
                <td style={{ border: '1px solid #ddd', padding: '0.5rem' }}>
                  {!task.completed && (
                    <button 
                      onClick={() => markComplete(task.id)}
                      style={{ padding: '0.25rem 0.5rem', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px' }}
                    >
                      Complete
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <AuthGuard>
      <TaskContent />
    </AuthGuard>
  );
};

export default Tasks;
