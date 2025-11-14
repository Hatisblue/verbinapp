import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Add, Delete } from '@mui/icons-material';
import { booksService } from '../../services/books';

interface Block {
  id: string;
  type: string;
  content: string;
  order: number;
}

const BookEditor: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [showGenerateDialog, setShowGenerateDialog] = useState(false);
  const [generatePrompt, setGeneratePrompt] = useState('');
  const [loading, setLoading] = useState(false);

  const addBlock = () => {
    const newBlock: Block = {
      id: Date.now().toString(),
      type: 'text',
      content: '',
      order: blocks.length,
    };
    setBlocks([...blocks, newBlock]);
  };

  const updateBlock = (id: string, content: string) => {
    setBlocks(blocks.map(b => b.id === id ? { ...b, content } : b));
  };

  const deleteBlock = (id: string) => {
    setBlocks(blocks.filter(b => b.id !== id));
  };

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await booksService.generateBook({
        plot: generatePrompt,
        language: 'ru',
        age_group: '7-12',
        pages: 5,
        style: 'сказка',
      });
      alert('Книга сгенерирована! ID: ' + result.book_id);
      setShowGenerateDialog(false);
    } catch (error) {
      alert('Ошибка генерации');
    } finally {
      setLoading(false);
    }
  };

  const saveBook = async () => {
    try {
      await booksService.createBook({ title, description });
      alert('Книга сохранена!');
    } catch (error) {
      alert('Ошибка сохранения');
    }
  };

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 2 }}>
        <Typography variant="h5" gutterBottom>
          Редактор книги
        </Typography>
        <TextField
          fullWidth
          label="Название книги"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          margin="normal"
        />
        <TextField
          fullWidth
          multiline
          rows={3}
          label="Описание"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          margin="normal"
        />
        <Box sx={{ mt: 2 }}>
          <Button variant="contained" color="primary" onClick={saveBook} sx={{ mr: 1 }}>
            Сохранить
          </Button>
          <Button variant="outlined" onClick={() => setShowGenerateDialog(true)}>
            Генерировать с AI
          </Button>
        </Box>
      </Paper>

      {blocks.map((block) => (
        <Paper key={block.id} sx={{ p: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'start' }}>
            <TextField
              fullWidth
              multiline
              rows={4}
              value={block.content}
              onChange={(e) => updateBlock(block.id, e.target.value)}
              placeholder="Содержимое блока..."
            />
            <IconButton onClick={() => deleteBlock(block.id)} color="error">
              <Delete />
            </IconButton>
          </Box>
        </Paper>
      ))}

      <Button
        fullWidth
        variant="outlined"
        startIcon={<Add />}
        onClick={addBlock}
        sx={{ mt: 2 }}
      >
        Добавить блок
      </Button>

      <Dialog open={showGenerateDialog} onClose={() => setShowGenerateDialog(false)}>
        <DialogTitle>Генерация книги с AI</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Опишите сюжет книги"
            value={generatePrompt}
            onChange={(e) => setGeneratePrompt(e.target.value)}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowGenerateDialog(false)}>Отмена</Button>
          <Button onClick={handleGenerate} variant="contained" disabled={loading}>
            {loading ? 'Генерация...' : 'Генерировать'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default BookEditor;
