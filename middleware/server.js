const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { GraphQLSchema, GraphQLObjectType, GraphQLString, GraphQLBoolean, GraphQLFloat, GraphQLInt, GraphQLList } = require('graphql');
const mysql = require('mysql2/promise');

const app = express();

// Create a MySQL connection pool
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'rootpass1',
  database: 'bookstore',
});

const AuthorType = new GraphQLObjectType({
  name: 'Author',
  fields: {
    author_id: { type: GraphQLInt },
    author_fname: { type: GraphQLString },
    author_lname: { type: GraphQLString },
    author_nl: {
      type: GraphQLBoolean,
      resolve: (parent) => {
        const value = (parent.author_nl.toString('utf-8'));
        return value == '1';
      },
    },
  },
});

const PublisherType = new GraphQLObjectType({
  name: 'Publisher',
  fields: {
    publisher_id: {type: GraphQLInt},
    publisher_name: {type: GraphQLString},
    publisher_address_id: {type: GraphQLInt}
  },
})

const AddressType = new GraphQLObjectType({
  name: 'Address',
  fields: {
    address_id: {type: GraphQLInt},
    address_one: {type: GraphQLString},
    address_two: {type: GraphQLString},
    city: {type: GraphQLString},
    state: {type: GraphQLString},
    zip: {type: GraphQLInt}
  },
})

const BPAAType = new GraphQLObjectType({
  name: 'BPAA',
  fields: {
    book_id: {type: GraphQLInt},
    book_name: {type: GraphQLString},
    book_author_id: {type: GraphQLInt},
    book_publisher_id: {type: GraphQLInt},
    book_price: {type: GraphQLFloat},
    book_isbn: {type: GraphQLString},
    book_nl: {
      type: GraphQLBoolean,
      resolve: (parent) => {
        const value = (parent.book_nl.toString('utf-8'));
        return value == '1';
      },
    },
    publisher_id: {type: GraphQLInt},
    publisher_name: {type: GraphQLString},
    publisher_address_id: {type: GraphQLInt},
    author_id: { type: GraphQLInt },
    author_fname: { type: GraphQLString },
    author_lname: { type: GraphQLString },
    author_nl: {
      type: GraphQLBoolean,
      resolve: (parent) => {
        const value = (parent.author_nl.toString('utf-8'));
        return value == '1';
      },
    },
    address_id: {type: GraphQLInt},
    address_one: {type: GraphQLString},
    address_two: {type: GraphQLString},
    city: {type: GraphQLString},
    state: {type: GraphQLString},
    zip: {type: GraphQLInt},
  },
})

const BookType = new GraphQLObjectType({
  name: 'Book',
  fields: {
    book_id: {type: GraphQLInt},
    book_name: {type: GraphQLString},
    book_author_id: {type: GraphQLInt},
    book_publisher_id: {type: GraphQLInt},
    book_price: {type: GraphQLFloat},
    book_isbn: {type: GraphQLString},
    book_nl: {
      type: GraphQLBoolean,
      resolve: (parent) => {
        const value = (parent.book_nl.toString('utf-8'));
        return value == '1';
      },
    },

  },
})
const PAType = new GraphQLObjectType ({
  name: 'PA',
  fields: {
    publisher_id: {type: GraphQLInt},
    publisher_name: {type: GraphQLString},
    address_id: {type: GraphQLInt},
    address_one: {type: GraphQLString},
    address_two: {type: GraphQLString},
    city: {type: GraphQLString},
    state: {type: GraphQLString},
    zip: {type: GraphQLInt},
  },

})

// Define a GraphQL schema
const schema = new GraphQLSchema({
  query: new GraphQLObjectType({
    name: 'Query',
    fields: {
      authors: {
        type: GraphQLList(AuthorType),
        args: {
          author_id: { type: GraphQLInt },
        },
        resolve: async(_, args) => {
          const {author_id} = args;
          let query = 'SELECT * FROM author ';
          if (author_id) {
            query += `WHERE author_id = ${author_id}`
            //console.log(query)
          }

          const [rows] = await pool.query(query);
          //console.log(rows)
          return rows;
        },
      },
      publishers: {
        type: GraphQLList(PublisherType),
        args: {
          publisher_id: {type: GraphQLInt},
        },
        resolve: async(_, args) => {
          const {publisher_id} = args;
          let query = 'SELECT * FROM publisher ';
          if (publisher_id) {
            query += `WHERE publisher_id = ${publisher_id}`
            //console.log(query)
          }
          const [rows] = await pool.query(query);
          //console.log(rows)
          return rows;
        },
      },
      addresses: {
        type: GraphQLList(AddressType),
        resolve: async () => {
          const [rows] = await pool.query('SELECT * FROM address');
          //console.log(rows)
          return rows;
        },
      },
      books: {
        type: GraphQLList(BookType),
        resolve: async () => {
          const [rows] = await pool.query('SELECT * FROM book');
          //console.log(rows)
          return rows;
        },
      },
      books_publishers_authors_addresses: {
        type: GraphQLList(BPAAType),
        resolve: async () => {
          const [rows] = await pool.query("SELECT * FROM ((((book b INNER JOIN publisher p ON b.book_publisher_id = p.publisher_id) INNER JOIN author a ON b.book_author_id = a.author_id) INNER JOIN address z ON p.publisher_address_id = z.address_id) INNER JOIN address y ON a.author_add1 = y.address_id);");
          //console.log(rows)
          return rows;
        },
      },
      publishers_addresses: {
        type: GraphQLList(PAType),
        resolve: async () => {
          const [rows] = await pool.query('SELECT * FROM publisher p INNER JOIN address a ON a.address_id = p.publisher_address_id;')
          return rows;
        }
      }
    },
  }),
});

// Create a GraphQL endpoint
app.use('/graphql', graphqlHTTP({ schema, graphiql: true }));

// Start the server
app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000/graphql');
});
