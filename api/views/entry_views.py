# rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status

# Django imports
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

# model and serializer import
from ..models.entry import Entry
from ..serializers import EntrySerializer, UserSerializer

# Views
class Entries(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = EntrySerializer

    # GET request
    def get(self, request):
        """'Index Entries request'"""
        entries = Entry.objects.filter(owner=request.user.id)
        data = EntrySerializer(entries, many=True).data
        return Response({ 'entries': data })

    # POST request
    def post(self, request):
        """'Create Entry request'"""
        # Add user to data object.
        request.data['entry']['creator'] = request.user.id
        # Create Entry
        entry = EntrySerializer(data=request.data['entry'])

        if entry.is_valid():
            entry.save()
            return Response({ 'entry': entry.data},
            status=status.HTTP_201_CREATED)

        return Response(entry.errors,
        status=status.HTTP_400_BAD_REQUEST)

class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    # Show request
    def get(self, request, pk):
        """'Show Entry request'"""
        # Locate the entry to show
        entry = get_object_or_404(Entry, pk=pk)
        # Only show owned Entries
        if not request.user.id == entry.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this entry')

        data = EntrySerializer(entry).data
        return Response({ 'entry': data })
    # DELETE Request
    def delete(self, request, pk):
        """'Delete Entry request'"""
        # Locate entry to delete
        entry = get_object_or_404(Entry, pk=pk)
        # check if requestor has permission.
        if not request.user.id == entry.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this entry.')
        # only delete if user owns the entry
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """'Update Entry request'"""
        if request.data['entry'].get('creator', False):
            del request.data['entry']['creator']

        entry = get_object_or_404(Entry, pk=pk)

        if not request.user.id == entry.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this entry!')

        request.data['entry']['creator'] = request.user.id

        data = EntrySerializer(entry, data=request.data['entry'])

        if data.is_valid():
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
