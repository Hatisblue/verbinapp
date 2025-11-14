import React from 'react';
import { Box, Typography, Grid, Card, CardContent } from '@mui/material';

const ShowcasePage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Витрина книг
      </Typography>
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {[1, 2, 3, 4, 5, 6].map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  Книга #{item}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Описание книги...
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ShowcasePage;
