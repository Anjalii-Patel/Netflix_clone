# backend/users/views.py
from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from django.utils import timezone
from .models import SubscriptionPlan, Subscription
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        full_name = request.data.get("full_name", "")

        if not username or not password or not email or not full_name:
            return Response({"error": "All fields required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username taken"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password, full_name=full_name)
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello {request.user.username}, you are authenticated!"})

class PlanListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = SubscriptionPlan.objects.all()
    def list(self, request, *args, **kwargs):
        data = [{"id": p.id, "name": p.name, "price": str(p.price), "duration_days": p.duration_days, "description": p.description} for p in self.get_queryset()]
        return Response(data)

class SubscribeCheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        plan_id = request.data.get("plan_id")
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({"detail": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()
        # deactivate existing
        Subscription.objects.filter(user=request.user, active=True).update(active=False)
        # create new
        sub = Subscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=now,
            end_date=now + timezone.timedelta(days=plan.duration_days),
            active=True
        )
        return Response({
            "message": "Subscription activated",
            "plan": plan.name,
            "active_until": sub.end_date
        })

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get("username")
        password = attrs.get("password")

        # If user typed email, resolve to username
        if identifier and "@" in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                attrs["username"] = user_obj.username
            except User.DoesNotExist:
                pass

        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
