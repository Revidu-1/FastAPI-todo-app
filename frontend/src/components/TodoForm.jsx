import { useState, useRef, useCallback } from 'react';
import Button from './Button';
import Input from './Input';
import './TodoForm.css';

/**
 * TodoForm component demonstrating:
 * - Props (onSubmit)
 * - useState for form state
 * - useRef to focus input after submission
 * - useCallback for memoized handlers
 */
const TodoForm = ({ onSubmit, loading = false }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const titleInputRef = useRef(null);

  // Handle form submission
  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      if (!title.trim()) return;

      try {
        await onSubmit({ title: title.trim(), description: description.trim() });
        // Reset form after successful submission
        setTitle('');
        setDescription('');
        // Focus back on title input
        titleInputRef.current?.focus();
      } catch (error) {
        // Error handling is done in parent component
      }
    },
    [title, description, onSubmit]
  );

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <Input
        ref={titleInputRef}
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Todo title..."
        maxLength={200}
        required
        className="todo-form-input"
      />
      <Input
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description (optional)..."
        maxLength={1000}
        className="todo-form-input"
      />
      <Button type="submit" variant="primary" disabled={loading || !title.trim()}>
        {loading ? 'Adding...' : 'Add Todo'}
      </Button>
    </form>
  );
};

export default TodoForm;




