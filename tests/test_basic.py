from app import create_app


def test_health_returns_successful_response():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "running", "database": "connected"}