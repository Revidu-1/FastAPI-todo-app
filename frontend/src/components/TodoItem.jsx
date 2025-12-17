import { useState, useRef, useCallback, useMemo } from 'react';
import Button from './Button';
import Input from './Input';
import './TodoItem.css';

/**
 * TodoItem component demonstrating:
 * - Props (todo, onUpdate, onDelete, onToggle)
 * - useState for local editing state
 * - useRef to focus input on edit
 * - useCallback to memoize handlers
 * - useMemo to compute derived values
 */
const TodoItem = ({ todo, onUpdate, onDelete, onToggle }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const titleInputRef = useRef(null);

  // Focus input when editing starts
  const handleStartEdit = useCallback(() => {
    setIsEditing(true);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    // Use setTimeout to ensure DOM is updated before focusing
    setTimeout(() => {
      titleInputRef.current?.focus();
    }, 0);
  }, [todo.title, todo.description]);

  // Cancel editing
  const handleCancelEdit = useCallback(() => {
    setIsEditing(false);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
  }, [todo.title, todo.description]);

  // Save edited todo
  const handleSave = useCallback(async () => {
    if (!editTitle.trim()) return;
    
    try {
      await onUpdate(todo.id, {
        title: editTitle.trim(),
        description: editDescription.trim(),
      });
      setIsEditing(false);
    } catch (error) {
      // Error handling is done in parent component
    }
  }, [editTitle, editDescription, todo.id, onUpdate]);

  // Handle toggle completion
  const handleToggle = useCallback(() => {
    onToggle(todo);
  }, [todo, onToggle]);

  // Handle delete
  const handleDelete = useCallback(() => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      onDelete(todo.id);
    }
  }, [todo.id, onDelete]);

  // Memoize computed className
  const itemClassName = useMemo(
    () => `todo-item ${todo.completed ? 'completed' : ''} ${isEditing ? 'editing' : ''}`,
    [todo.completed, isEditing]
  );

  // Memoize text className
  const textClassName = useMemo(
    () => (todo.completed ? 'strikethrough' : ''),
    [todo.completed]
  );

  if (isEditing) {
    return (
      <div className={itemClassName}>
        <div className="todo-edit-form">
          <Input
            ref={titleInputRef}
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            placeholder="Todo title..."
            maxLength={200}
            className="todo-edit-input"
          />
          <Input
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            placeholder="Description (optional)..."
            maxLength={1000}
            className="todo-edit-input"
          />
          <div className="todo-actions">
            <Button variant="success" onClick={handleSave}>
              Save
            </Button>
            <Button variant="secondary" onClick={handleCancelEdit}>
              Cancel
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={itemClassName}>
      <div className="todo-content">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={handleToggle}
          className="todo-checkbox"
          aria-label="Toggle todo completion"
        />
        <div className="todo-text">
          <h3 className={textClassName}>{todo.title}</h3>
          {todo.description && (
            <p className={textClassName}>{todo.description}</p>
          )}
        </div>
      </div>
      <div className="todo-actions">
        <Button variant="outline" onClick={handleStartEdit}>
          Edit
        </Button>
        <Button variant="danger" onClick={handleDelete}>
          Delete
        </Button>
      </div>
    </div>
  );
};

export default TodoItem;

