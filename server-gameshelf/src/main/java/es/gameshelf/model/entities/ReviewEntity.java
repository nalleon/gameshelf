package es.gameshelf.model.entities;

import java.util.Date;
import java.util.Objects;
import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
public class ReviewEntity {
    /**
     * Properties
     */
    private int id;
    private String content;
    private Date creationDate;
    private Date lastUpdateDate;
    private UserEntity userEntity;
    private GameEntity gameEntity;
    private Set<PhotoReviewEntity> photoReviewEntitySet;

    /**
     * Default constructor of the class
     */
    public ReviewEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the review
     */
    public ReviewEntity(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param userEntity of the review
     */
    public ReviewEntity(UserEntity userEntity) {
        this.userEntity = userEntity;
    }

    /**
     * Constructor of the class
     * @param gameEntity of the review
     */
    public ReviewEntity(GameEntity gameEntity) {
        this.gameEntity = gameEntity;
    }

    /**
     * Full constructor of the class
     * @param id of the review
     * @param content of the review
     * @param creationDate of the review
     * @param lastUpdateDate of the review
     * @param userEntity of the review
     * @param gameEntity of the review
     * @param photoReviewEntitySet of the review
     */
    public ReviewEntity(int id, String content, Date creationDate, Date lastUpdateDate, UserEntity userEntity,
                        GameEntity gameEntity, Set<PhotoReviewEntity> photoReviewEntitySet) {
        this.id = id;
        this.content = content;
        this.creationDate = creationDate;
        this.lastUpdateDate = lastUpdateDate;
        this.userEntity = userEntity;
        this.gameEntity = gameEntity;
        this.photoReviewEntitySet = photoReviewEntitySet;
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

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Date getCreationDate() {
        return creationDate;
    }

    public void setCreationDate(Date creationDate) {
        this.creationDate = creationDate;
    }

    public Date getLastUpdateDate() {
        return lastUpdateDate;
    }

    public void setLastUpdateDate(Date lastUpdateDate) {
        this.lastUpdateDate = lastUpdateDate;
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

    public Set<PhotoReviewEntity> getPhotoReviewSet() {
        return photoReviewEntitySet;
    }

    public void setPhotoReviewSet(Set<PhotoReviewEntity> photoReviewEntitySet) {
        this.photoReviewEntitySet = photoReviewEntitySet;
    }

    /**
     * Equals and hashcode
     */
    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        ReviewEntity reviewEntity = (ReviewEntity) o;
        return id == reviewEntity.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "ReviewEntity{" +
                "id=" + id +
                ", content='" + content + '\'' +
                ", creationDate=" + creationDate +
                ", lastUpdateDate=" + lastUpdateDate +
                ", userEntity=" + userEntity +
                ", gameEntity=" + gameEntity +
                ", photoReviewEntitySet=" + photoReviewEntitySet +
                '}';
    }
}
