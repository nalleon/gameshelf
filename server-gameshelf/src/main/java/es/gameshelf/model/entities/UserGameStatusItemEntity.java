package es.gameshelf.model.entities;

import java.util.Date;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class UserGameStatusItemEntity {

    /**
     * Properties
     */
    private int id;
    private float userRating;
    private Date startDate;
    private Date endDate;
    private String annotation;
    private UserEntity userEntity;
    private GameEntity gameEntity;
    private StatusEntity statusEntity;

    /**
     * Default constructor of the class
     */
    public UserGameStatusItemEntity() {
    }

    /**
     * Constructor of the class
     * @param id of UserGameStatusItemEntity
     */
    public UserGameStatusItemEntity(int id) {
        this.id = id;
    }

    /**
     * Full constructor of the class
     * @param id of UserGameStatusItemEntity
     * @param userRating of UserGameStatusItemEntity
     * @param startDate of UserGameStatusItemEntity
     * @param endDate of UserGameStatusItemEntity
     * @param annotation of UserGameStatusItemEntity
     * @param userEntity of UserGameStatusItemEntity
     * @param gameEntity of UserGameStatusItemEntity
     * @param statusEntity of UserGameStatusItemEntity
     */
    public UserGameStatusItemEntity(int id, float userRating, Date startDate, Date endDate, String annotation,
                                    UserEntity userEntity, GameEntity gameEntity, StatusEntity statusEntity) {
        this.id = id;
        this.userRating = userRating;
        this.startDate = startDate;
        this.endDate = endDate;
        this.annotation = annotation;
        this.userEntity = userEntity;
        this.gameEntity = gameEntity;
        this.statusEntity = statusEntity;
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

    public Date getEndDate() {
        return endDate;
    }

    public void setEndDate(Date endDate) {
        this.endDate = endDate;
    }

    public String getAnnotation() {
        return annotation;
    }

    public void setAnnotation(String annotation) {
        this.annotation = annotation;
    }

    public UserEntity getUser() {
        return userEntity;
    }

    public void setUser(UserEntity userEntity) {
        this.userEntity = userEntity;
    }

    public GameEntity getGame() {
        return gameEntity;
    }

    public void setGame(GameEntity gameEntity) {
        this.gameEntity = gameEntity;
    }

    public StatusEntity getStatus() {
        return statusEntity;
    }

    public void setStatus(StatusEntity statusEntity) {
        this.statusEntity = statusEntity;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        UserGameStatusItemEntity that = (UserGameStatusItemEntity) o;
        return id == that.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "UserGameStatusItemEntity{" +
                "id=" + id +
                ", userRating=" + userRating +
                ", startDate=" + startDate +
                ", finishDate=" + endDate +
                ", annotation='" + annotation + '\'' +
                ", userEntity=" + userEntity +
                ", gameEntity=" + gameEntity +
                ", statusEntity=" + statusEntity +
                '}';
    }
}
