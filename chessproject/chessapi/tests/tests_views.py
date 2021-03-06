from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from chessproject.chessapi.models import Piece


class PiecesViewTestCase(APITestCase):
    def test_create_a_new_piece(self):
        """
        Ensures that is possible to create a new piece
        """
        url = reverse('pieces')
        data = {'type': 'Knight', 'color': 'white'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Piece.objects.count(), 1)

    def test_that_is_not_possible_create_an_invalid_piece(self):
        """
        Ensures that is not possible to create an invalid piece
        """
        url = reverse('pieces')
        data = {'type': 'Turtle', 'color': 'purple'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_that_the_moves_for_a_knight_are_returned_correctly(self):
        """
        Ensures that the moves for piece of the type Knight are returned
        """
        piece = Piece.objects.create(type='Knight', color='white')
        url = reverse('moves', kwargs={'pk': piece.id})
        data = {'coordinate': 'h1'}
        response = self.client.get(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(['d3', 'e2', 'e4', 'f2', 'f5', 'g3', 'g4', 'h3', 'h5'], response.data)

    def test_that_the_moves_for_a_different_piece_are_not_returned(self):
        """
        Ensures that the moves are not returned from a piece that is not a Knight
        """
        piece = Piece.objects.create(type='Queen', color='white')
        url = reverse('moves', kwargs={'pk': piece.id})
        data = {'coordinate': 'h1'}
        response = self.client.get(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data)

    def test_that_the_an_error_is_returned_when_a_position_is_not_provided(self):
        """
        Ensures that an status code 400 is returned when the argument position is not provided
        """
        piece = Piece.objects.create(type='Knight', color='white')
        url = reverse('moves', kwargs={'pk': piece.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
