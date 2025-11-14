import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const EditorPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Редактор книги
      </Typography>
      <Paper sx={{ p: 3, mt: 2 }}>
        <Typography variant="body1">
          Здесь будет Notion-подобный редактор книг...
        </Typography>
      </Paper>
    </Box>
  );
};

export default EditorPage;
