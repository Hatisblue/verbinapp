import api from './api';

export interface Book {
  id: number;
  title: string;
  description: string;
  cover_url: string;
  likes_count: number;
  views_count: number;
  is_published: boolean;
}

export const booksService = {
  getBooks: async (params?: any) => {
    const response = await api.get('/api/books', { params });
    return response.data;
  },

  getBook: async (id: number) => {
    const response = await api.get(`/api/books/${id}`);
    return response.data;
  },

  createBook: async (data: any) => {
    const response = await api.post('/api/books', data);
    return response.data;
  },

  updateBook: async (id: number, data: any) => {
    const response = await api.put(`/api/books/${id}`, data);
    return response.data;
  },

  deleteBook: async (id: number) => {
    await api.delete(`/api/books/${id}`);
  },

  publishBook: async (id: number) => {
    const response = await api.post(`/api/books/${id}/publish`);
    return response.data;
  },

  generateBook: async (data: any) => {
    const response = await api.post('/api/books/generate', data);
    return response.data;
  },

  likeBook: async (id: number) => {
    const response = await api.post(`/api/books/${id}/like`);
    return response.data;
  },

  unlikeBook: async (id: number) => {
    const response = await api.delete(`/api/books/${id}/like`);
    return response.data;
  },
};
