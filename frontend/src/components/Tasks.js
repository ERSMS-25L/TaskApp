import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ title: '', description: '', due_date: '', user_id: '' });

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_TASK_SERVICE_URL}/api/tasks/`);
      setTasks(response.data);
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
        user_id: Number(form.user_id)
      });
      setForm({ title: '', description: '', due_date: '', user_id: '' });
      fetchTasks();
    } catch (err) {
      console.error('Error creating task:', err);
      setError(err);
    }
  };

  const markComplete = async (id) => {
    try {
      await axios.put(`${process.env.REACT_APP_TASK_SERVICE_URL}/api/tasks/${id}`, { completed: true });
      fetchTasks();
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

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
        <input name="title" placeholder="Title" value={form.title} onChange={handleChange} required />
        <input name="description" placeholder="Description" value={form.description} onChange={handleChange} />
        <input name="due_date" placeholder="Due Date (YYYY-MM-DD)" value={form.due_date} onChange={handleChange} />
        <input name="user_id" placeholder="User ID" value={form.user_id} onChange={handleChange} required />
        <button type="submit">Add Task</button>
      </form>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
            <th>Due Date</th>
            <th>Completed</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map(task => (
            <tr key={task.id}>
              <td>{task.id}</td>
              <td>{task.title}</td>
              <td>{task.description}</td>
              <td>{task.due_date ? task.due_date : '-'}</td>
              <td>{task.completed ? 'Yes' : 'No'}</td>
              <td>
                {!task.completed && <button onClick={() => markComplete(task.id)}>Complete</button>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Tasks;
