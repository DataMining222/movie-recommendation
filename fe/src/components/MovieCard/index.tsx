import styles from "./index.module.css";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import FavoriteIcon from "@material-ui/icons/Favorite";
import CalendarToday from "@material-ui/icons/CalendarToday";
import { useHistory } from "react-router";

export type MovieCardProps = {
  title: string;
  year: string;
  imdb_id: string;
  image: string;
};

const MovieCard = ({ title, year, imdb_id, image }: MovieCardProps) => {
  return (
    <Card className={styles.root}>
      <CardActionArea className={styles.cardArea}>
        <CardMedia
          component="img"
          alt={title}
          height="400"
          image={image}
          title={title}
          className={styles.poster}
        />
        <CardContent className={styles.overText}>
          <h2>{title}</h2>
        </CardContent>
      </CardActionArea>
      <CardActions className={styles.actionsContainer}>
        <Typography gutterBottom component="i" className={styles.yearSection}>
          <CalendarToday fontSize="small" />
          &nbsp;
          {year}
        </Typography>
        <IconButton aria-label="add to favorites">
          <FavoriteIcon />
        </IconButton>
      </CardActions>
    </Card>
  );
};

export default MovieCard;
