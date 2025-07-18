package es.gameshelf.model.entities;

import java.util.Date;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class GameScoreEntity {
    /**
     * Properties
     */
    private int id;
    private float score;
    private Date lastUpdate;
    private UserEntity userEntity;
    private GameEntity gameEntity;

    /**
     * Default constructor of the class
     */
    public GameScoreEntity() {
    }

    /**
     * Constructor of the class
     * @param id of GameScoreEntity
     */
    public GameScoreEntity(int id) {
        this.id = id;
    }

    /**
     * Full constructor of the class
     * @param id of GameScoreEntity
     * @param score of GameScoreEntity
     * @param lastUpdate of GameScoreEntity
     * @param userEntity of GameScoreEntity
     * @param gameEntity of GameScoreEntity
     */
    public GameScoreEntity(int id, float score, Date lastUpdate, UserEntity userEntity, GameEntity gameEntity) {
        this.id = id;
        this.score = score;
        this.lastUpdate = lastUpdate;
        this.userEntity = userEntity;
        this.gameEntity = gameEntity;
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

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        GameScoreEntity gameScoreEntity = (GameScoreEntity) o;
        return id == gameScoreEntity.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "GameScoreEntity{" +
                "id=" + id +
                ", score=" + score +
                ", lastUpdate=" + lastUpdate +
                ", userEntity=" + userEntity +
                ", gameEntity=" + gameEntity +
                '}';
    }
}
