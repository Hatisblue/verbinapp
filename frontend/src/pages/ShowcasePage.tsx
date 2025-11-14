import React, { useState, useEffect } from 'react';
import { Box, Typography, Grid, Card, CardContent, CardMedia, CardActions, Button, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { booksService, Book } from '../services/books';

const ShowcasePage: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    try {
      const data = await booksService.getBooks({ limit: 20 });
      setBooks(data);
    } catch (error) {
      console.error('Failed to load books', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
      <CircularProgress />
    </Box>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Витрина книг
      </Typography>
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {books.map((book) => (
          <Grid item xs={12} sm={6} md={4} key={book.id}>
            <Card>
              {book.cover_url && (
                <CardMedia
                  component="img"
                  height="200"
                  image={book.cover_url}
                  alt={book.title}
                />
              )}
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {book.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {book.description?.substring(0, 100)}...
                </Typography>
                <Box sx={{ mt: 1 }}>
                  <Typography variant="caption" color="text.secondary">
                    👁 {book.views_count} | ❤️ {book.likes_count}
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => navigate(`/book/${book.id}`)}>
                  Читать
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ShowcasePage;
