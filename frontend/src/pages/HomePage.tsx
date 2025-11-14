import React from 'react';
import { Box, Typography, Button, Container, Grid, Card, CardContent } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          py: 8,
          mb: 4,
          borderRadius: 2,
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h2" component="h1" gutterBottom align="center">
            Создавайте книги с помощью ИИ
          </Typography>
          <Typography variant="h5" align="center" paragraph>
            AI BookCreator — платформа для создания, редактирования и публикации книг
            с использованием искусственного интеллекта Google Gemini
          </Typography>
          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center', gap: 2 }}>
            <Button
              variant="contained"
              color="secondary"
              size="large"
              component={RouterLink}
              to="/editor"
            >
              Создать книгу
            </Button>
            <Button
              variant="outlined"
              color="inherit"
              size="large"
              component={RouterLink}
              to="/showcase"
            >
              Посмотреть книги
            </Button>
          </Box>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ my: 8 }}>
        <Typography variant="h3" gutterBottom align="center">
          Возможности платформы
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Генерация контента
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Создавайте книги с помощью AI на основе вашего сюжета.
                  Gemini генерирует текст, изображения и даже озвучку!
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Notion-подобный редактор
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Удобный блочный редактор для создания и редактирования
                  книг с поддержкой текста, изображений, аудио и видео.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Публикация и витрина
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Публикуйте свои книги и делитесь ими с миром.
                  Получайте лайки, комментарии и участвуйте в челленджах!
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* Popular Books Section */}
      <Container maxWidth="lg" sx={{ my: 8 }}>
        <Typography variant="h3" gutterBottom align="center">
          Популярные книги
        </Typography>
        <Typography variant="body1" align="center" color="text.secondary">
          Здесь будут отображаться популярные книги...
        </Typography>
      </Container>
    </Box>
  );
};

export default HomePage;
