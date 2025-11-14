import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const ViewerPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Просмотр книги
      </Typography>
      <Paper sx={{ p: 3, mt: 2 }}>
        <Typography variant="body1">
          Здесь будет просмотр книги...
        </Typography>
      </Paper>
    </Box>
  );
};

export default ViewerPage;
