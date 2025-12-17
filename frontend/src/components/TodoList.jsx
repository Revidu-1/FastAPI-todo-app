import { useMemo } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTodos } from '../hooks/useTodos';
import TodoForm from './TodoForm';
import TodoItem from './TodoItem';
import Button from './Button';
import './TodoList.css';

/**
 * TodoList component demonstrating:
 * - Props (none, uses hooks and context)
 * - Custom hooks (useAuth, useTodos)
 * - useMemo for computed values
 * - Component composition with TodoForm and TodoItem
 */
function TodoList() {
  const { logout } = useAuth();
  const {
    todos,
    loading,
    error,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleComplete,
  } = useTodos();

  // Memoize sorted todos (completed at bottom)
  const sortedTodos = useMemo(() => {
    return [...todos].sort((a, b) => {
      if (a.completed === b.completed) {
        return b.id - a.id; // Newer first
      }
      return a.completed ? 1 : -1; // Incomplete first
    });
  }, [todos]);

  // Memoize stats
  const stats = useMemo(() => {
    const total = todos.length;
    const completed = todos.filter((t) => t.completed).length;
    const remaining = total - completed;
    return { total, completed, remaining };
  }, [todos]);

  return (
    <div className="todo-container">
      <div className="todo-header">
        <div>
          <h1>My Todos</h1>
          {stats.total > 0 && (
            <p className="todo-stats">
              {stats.remaining} remaining, {stats.completed} completed
            </p>
          )}
        </div>
        <Button variant="outline" onClick={logout}>
          Logout
        </Button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <TodoForm onSubmit={createTodo} loading={loading} />

      {loading && todos.length === 0 ? (
        <div className="loading">Loading todos...</div>
      ) : sortedTodos.length === 0 ? (
        <div className="empty-state">
          <p>No todos yet. Create one above!</p>
        </div>
      ) : (
        <div className="todo-list">
          {sortedTodos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onUpdate={updateTodo}
              onDelete={deleteTodo}
              onToggle={toggleComplete}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default TodoList;
