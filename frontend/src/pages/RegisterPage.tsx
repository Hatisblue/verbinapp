import React from 'react';
import { Box, Typography, TextField, Button, Paper, Container } from '@mui/material';

const RegisterPage: React.FC = () => {
  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom align="center">
          Регистрация
        </Typography>
        <Box component="form" sx={{ mt: 2 }}>
          <TextField
            fullWidth
            label="Имя пользователя"
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Email"
            type="email"
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Пароль"
            type="password"
            margin="normal"
            required
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3 }}
          >
            Зарегистрироваться
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default RegisterPage;
