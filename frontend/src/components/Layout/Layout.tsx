import React, { useEffect, useState } from 'react';
import { Box, Container, AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { authService } from '../../services/auth';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isAuth, setIsAuth] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setIsAuth(authService.isAuthenticated());
  }, []);

  const handleLogout = () => {
    authService.logout();
    setIsAuth(false);
    navigate('/');
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AI BookCreator
          </Typography>
          <Button color="inherit" component={RouterLink} to="/">
            Главная
          </Button>
          <Button color="inherit" component={RouterLink} to="/showcase">
            Витрина
          </Button>
          {isAuth && (
            <Button color="inherit" component={RouterLink} to="/editor">
              Создать книгу
            </Button>
          )}
          {isAuth ? (
            <Button color="inherit" onClick={handleLogout}>
              Выйти
            </Button>
          ) : (
            <Button color="inherit" component={RouterLink} to="/login">
              Войти
            </Button>
          )}
        </Toolbar>
      </AppBar>

      <Container component="main" sx={{ flex: 1, py: 4 }}>
        {children}
      </Container>

      <Box component="footer" sx={{ bgcolor: 'background.paper', py: 3, mt: 'auto' }}>
        <Container maxWidth="lg">
          <Typography variant="body2" color="text.secondary" align="center">
            © 2025 AI BookCreator. Все права защищены.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;
