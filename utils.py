from pathlib import Path

def execute_sql(
    string,
    engine,
    read_file=True,
    print_=False,
    return_df=False,
    chunksize=None,
    params=None,
):
    """
    Executes a SQL query from a file or a string using SQLAlchemy engine
    Note: Must only be basic SQL (e.g. does not run PSQL \copy and other commands)
    Note: SQL file CANNOT START WITH A COMMENT! There can be comments later on in the file, but for some reason
    doesn't work if you start with one (seems to treat the entire file as commented)
    Parameters
    ----------
    string : string
        Either a filename (with full path string '.../.../.sql') or a specific query string to be executed
        Can include "parameters" (in the form of {param_name}) whose values are filled in at the time of execution
    engine : SQLAlchemy engine object
        To connect to DB
    read_file : boolean
        Whether to treat the string as a filename or a query
    print_ : boolean
        Whether to print the 'Executed query' statement
    return_df : boolean
        Whether to return the result table of query as a Pandas dataframe
    chunksize : int
        Rows will be read in batches of this size at a time; all rows will be read at once if not specified
    params : dict
        In the case of parameterized SQL, the dictionary of parameters in the form of {'param_name': param_value}
    Returns
    -------
    ResultProxy : ResultProxy
        see SQLAlchemy documentation; results of query
    """

    if read_file:
        query = string.read_text()
    else:
        query = string

    if params is not None:
        query = query.format(**params)

    if print_:
        print("Query executed")

    if return_df:
        res_df = pd.read_sql_query(query, engine, chunksize=chunksize)
        return res_df
    else:  # Not all result objects return rows.
        engine.execute(query)
