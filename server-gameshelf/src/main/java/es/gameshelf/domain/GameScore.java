package es.gameshelf.domain;

import java.util.Date;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class GameScore {
    /**
     * Properties
     */
    private int id;
    private float score;
    private Date lastUpdate;
    private User user;
    private Game game;

    /**
     * Default constructor of the class
     */
    public GameScore() {
    }

    /**
     * Constructor of the class
     * @param id of GameScore
     */
    public GameScore(int id) {
        this.id = id;
    }

    /**
     * Full constructor of the class
     * @param id of GameScore
     * @param score of GameScore
     * @param lastUpdate of GameScore
     * @param user of GameScore
     * @param game of GameScore
     */
    public GameScore(int id, float score, Date lastUpdate, User user, Game game) {
        this.id = id;
        this.score = score;
        this.lastUpdate = lastUpdate;
        this.user = user;
        this.game = game;
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

    public float getScore() {
        return score;
    }

    public void setScore(float score) {
        this.score = score;
    }

    public Date getLastUpdate() {
        return lastUpdate;
    }

    public void setLastUpdate(Date lastUpdate) {
        this.lastUpdate = lastUpdate;
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

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        GameScore gameScore = (GameScore) o;
        return id == gameScore.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "GameScore{" +
                "id=" + id +
                ", score=" + score +
                ", lastUpdate=" + lastUpdate +
                ", user=" + user +
                ", game=" + game +
                '}';
    }
}
