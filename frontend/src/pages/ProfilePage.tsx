import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const ProfilePage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Профиль пользователя
      </Typography>
      <Paper sx={{ p: 3, mt: 2 }}>
        <Typography variant="body1">
          Здесь будет профиль пользователя...
        </Typography>
      </Paper>
    </Box>
  );
};

export default ProfilePage;
