package es.gameshelf.domain;

import java.util.Date;
import java.util.Objects;
import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
public class Review {
    /**
     * Properties
     */
    private int id;
    private String content;
    private Date creationDate;
    private Date lastUpdateDate;
    private User user;
    private Game game;
    private Set<PhotoReview> photoReviewSet;

    /**
     * Default constructor of the class
     */
    public Review() {
    }

    /**
     * Constructor of the class
     * @param id of the review
     */
    public Review(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param user of the review
     */
    public Review(User user) {
        this.user = user;
    }

    /**
     * Constructor of the class
     * @param game of the review
     */
    public Review(Game game) {
        this.game = game;
    }

    /**
     * Full constructor of the class
     * @param id of the review
     * @param content of the review
     * @param creationDate of the review
     * @param lastUpdateDate of the review
     * @param user of the review
     * @param game of the review
     * @param photoReviewSet of the review
     */
    public Review(int id, String content, Date creationDate, Date lastUpdateDate, User user,
                  Game game, Set<PhotoReview> photoReviewSet) {
        this.id = id;
        this.content = content;
        this.creationDate = creationDate;
        this.lastUpdateDate = lastUpdateDate;
        this.user = user;
        this.game = game;
        this.photoReviewSet = photoReviewSet;
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

    public Set<PhotoReview> getPhotoReviewSet() {
        return photoReviewSet;
    }

    public void setPhotoReviewSet(Set<PhotoReview> photoReviewSet) {
        this.photoReviewSet = photoReviewSet;
    }

    /**
     * Equals and hashcode
     */
    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Review review = (Review) o;
        return id == review.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "Review{" +
                "id=" + id +
                ", content='" + content + '\'' +
                ", creationDate=" + creationDate +
                ", lastUpdateDate=" + lastUpdateDate +
                ", user=" + user +
                ", game=" + game +
                ", photoReviewSet=" + photoReviewSet +
                '}';
    }
}
