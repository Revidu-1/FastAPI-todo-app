import { useState, useEffect, useCallback } from 'react';
import { todoAPI } from '../api/client';

/**
 * Custom hook to manage todos
 */
export const useTodos = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load todos from API
  const loadTodos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await todoAPI.getAll();
      setTodos(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load todos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Load todos on mount
  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  // Create a new todo
  const createTodo = useCallback(async (todoData) => {
    try {
      setError(null);
      const created = await todoAPI.create(todoData);
      setTodos((prevTodos) => [...prevTodos, created]);
      return created;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to create todo';
      setError(errorMsg);
      throw err;
    }
  }, []);

  // Update a todo
  const updateTodo = useCallback(async (id, todoData) => {
    try {
      setError(null);
      const updated = await todoAPI.update(id, todoData);
      setTodos((prevTodos) =>
        prevTodos.map((todo) => (todo.id === id ? updated : todo))
      );
      return updated;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to update todo';
      setError(errorMsg);
      throw err;
    }
  }, []);

  // Delete a todo
  const deleteTodo = useCallback(async (id) => {
    try {
      setError(null);
      await todoAPI.delete(id);
      setTodos((prevTodos) => prevTodos.filter((todo) => todo.id !== id));
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to delete todo';
      setError(errorMsg);
      throw err;
    }
  }, []);

  // Toggle todo completion
  const toggleComplete = useCallback(
    async (todo) => {
      await updateTodo(todo.id, { completed: !todo.completed });
    },
    [updateTodo]
  );

  return {
    todos,
    loading,
    error,
    loadTodos,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleComplete,
  };
};

