package es.gameshelf.domain;

import java.util.Date;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class UserGameStatusItem {

    /**
     * Properties
     */
    private int id;
    private float userRating;
    private Date startDate;
    private Date finishDate;
    private String annotation;
    private User user;
    private Game game;
    private Status status;

    /**
     * Default constructor of the class
     */
    public UserGameStatusItem() {
    }

    /**
     * Constructor of the class
     * @param id of UserGameStatusItem
     */
    public UserGameStatusItem(int id) {
        this.id = id;
    }

    /**
     * Full constructor of the class
     * @param id of UserGameStatusItem
     * @param userRating of UserGameStatusItem
     * @param startDate of UserGameStatusItem
     * @param finishDate of UserGameStatusItem
     * @param annotation of UserGameStatusItem
     * @param user of UserGameStatusItem
     * @param game of UserGameStatusItem
     * @param status of UserGameStatusItem
     */
    public UserGameStatusItem(int id, float userRating, Date startDate, Date finishDate, String annotation,
                              User user, Game game, Status status) {
        this.id = id;
        this.userRating = userRating;
        this.startDate = startDate;
        this.finishDate = finishDate;
        this.annotation = annotation;
        this.user = user;
        this.game = game;
        this.status = status;
    }

    /**
     * Getters and setters
     */
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public float getUserRating() {
        return userRating;
    }

    public void setUserRating(float userRating) {
        this.userRating = userRating;
    }

    public Date getStartDate() {
        return startDate;
    }

    public void setStartDate(Date startDate) {
        this.startDate = startDate;
    }

    public Date getFinishDate() {
        return finishDate;
    }

    public void setFinishDate(Date finishDate) {
        this.finishDate = finishDate;
    }

    public String getAnnotation() {
        return annotation;
    }

    public void setAnnotation(String annotation) {
        this.annotation = annotation;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Game getGame() {
        return game;
    }

    public void setGame(Game game) {
        this.game = game;
    }

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        UserGameStatusItem that = (UserGameStatusItem) o;
        return id == that.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "UserGameStatusItem{" +
                "id=" + id +
                ", userRating=" + userRating +
                ", startDate=" + startDate +
                ", finishDate=" + finishDate +
                ", annotation='" + annotation + '\'' +
                ", user=" + user +
                ", game=" + game +
                ", status=" + status +
                '}';
    }
}
