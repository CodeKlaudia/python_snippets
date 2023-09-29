def get_engine_cursor(username='',password=''):
    @contextmanager
    def conn_objects_generator(engine_obj=False):
        conn_string = oracledb.makedsn("sltdfrora014a", 10201, "OLT014BA")
        print(conn_string)
        conn = None
        try:
            conn = oracledb.connect(
                    user=username,
                    password=password,
                    dsn=conn_string
            )
            engine = create_engine("oracle+oracledb://", creator=lambda: conn,
                                   connect_args={"gopreload": True, "auto_convert": True})
            with engine.connect() as connection:
                cursor = connection.connection.cursor()
                try:
                    if engine_obj:
                        yield engine, cursor
                    else:
                        yield cursor
                    connection.commit()
                    print("worked")
                except:
                    connection.rollback()
                    print("not worked")
                    raise
                finally:
                    cursor.close()
                connection.close()
        except oracledb.DatabaseError as error:
            raise oracledb.DatabaseError(
                "Wrong connection credentials.", error) from error
        finally:
            if conn:
                conn.close()
    return conn_objects_generator
