import graphene
import graphql_jwt
from users import schema as UsersSchema


class Mutation(UsersSchema.Mutation, graphene.ObjectType):
    pass


class Query(UsersSchema.Query, graphene.ObjectType):
    # Example query for a dummy field
    hello = graphene.String()

    def resolve_hello(self, info):
        return "Hello, World!"


# Create schema
schema = graphene.Schema(query=Query, mutation=Mutation)
