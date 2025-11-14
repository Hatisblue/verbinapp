import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  return (
    <Box sx={{ textAlign: 'center', py: 8 }}>
      <Typography variant="h1" gutterBottom>
        404
      </Typography>
      <Typography variant="h5" gutterBottom>
        Страница не найдена
      </Typography>
      <Button
        variant="contained"
        component={RouterLink}
        to="/"
        sx={{ mt: 3 }}
      >
        На главную
      </Button>
    </Box>
  );
};

export default NotFoundPage;
