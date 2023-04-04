import { useState, useEffect, ReactElement } from "react";
import styles from "./index.module.css";
import SearchBox from "components/SearchBox";
import service from "utils/service";
import CONSTANTS from "utils/constants";
import MovieCard, { MovieCardProps } from "components/MovieCard";
import Skeleton from "components/MovieCard/Skeleton";
import { Grid, Select, MenuItem, FormControl } from "@material-ui/core";

const Home = (): ReactElement => {
  const [searchText, setSearchText] = useState("Comedy"); // Initial value set to 'man' to display default search results on UI
  const [select, setSelect] = useState("simple");
  const [movies, setMovies] = useState({ Search: [] });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    setIsLoading(false);
  }, [movies]);

  useEffect(() => {
    setIsLoading(true);
    const fetchMovies = async () => {
      const data = await service.get(CONSTANTS.BASE_URL, select, searchText);
      setMovies(data);
    };
    try {
      fetchMovies();
    } catch (e) {
      setError("Error occured! Cannot fetch!");
    }
  }, []);

  const handleSearch = async (text: string) => {
    setSearchText(text);
    setIsLoading(true);
    let searchedMovies;
    try {
      searchedMovies = await service.get(CONSTANTS.BASE_URL, select, text);
    } catch (e) {
      setError("Error occured! Cannot fetch!");
      setIsLoading(false);
    }
    setMovies(searchedMovies);
  };

  const handleSelectChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelect(event.target.value as string);
  };

  const MoviesLoader = (itemCount: number): ReactElement => {
    return (
      <Grid container spacing={2}>
        {[...new Array(itemCount)].map((_, i: number) => (
          <Grid item xs={12} md={3} key={i}>
            <Skeleton />
          </Grid>
        ))}
      </Grid>
    );
  };

  return (
    <div className={styles.root}>
      <Grid container justify="center">
        <Grid item xs={12} sm={10}>
          <Grid container justify="center">
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  label="Age"
                  defaultValue={select}
                  onChange={handleSelectChange}
                >
                  <MenuItem value={"simple"}>Simple</MenuItem>
                  <MenuItem value={"content"}>Content Based</MenuItem>
                  <MenuItem value={"hybrid"}>Hybrid</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <SearchBox className={styles.searchBox} onSearch={handleSearch} />
            </Grid>
          </Grid>

          <Grid item xs={12} className={styles.movieListContainer}>
            {/* Loading state */}
            {isLoading && MoviesLoader(8)}

            {/* Success state */}
            {!!movies ? (
              <Grid container spacing={2}>
                {movies.Search.map(
                  ({ title, imdb_id, year, image }: MovieCardProps) => (
                    <Grid item xs={12} md={3} key={imdb_id}>
                      <MovieCard {...{ title, imdb_id, year, image }} />
                    </Grid>
                  )
                )}
              </Grid>
            ) : (
              "No Result"
            )}

            {/* Error state */}
            {!!error && (
              <div className={styles.errorMessageContainer}>
                {JSON.stringify(error)}
              </div>
            )}
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
};

export default Home;
