package es.gameshelf.model.entities;

import jakarta.persistence.*;

import java.util.Objects;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
@Entity
@Table(name="favorites")
@NamedQuery(name="FavoriteEntity.findAll", query="SELECT r FROM FavoriteEntity r")
public class FavoriteEntity {

    /**
     * Properties
     */
    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
    @Column(unique=true, nullable=false)
    private int id;
    @ManyToOne()
    @JoinColumn(nullable=false, name = "user_id")
    private UserEntity userEntity;

    @ManyToOne()
    @JoinColumn(nullable=false, name = "game_id")
    private GameEntity gameEntity;

    /**
     * Default constructor of the class
     */
    public FavoriteEntity() {}

    /**
     * Constructor of the class
     * @param id of the favorite
     */
    public FavoriteEntity(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param userEntity of the favorite
     * @param gameEntity of the favorite
     * @implNote for creating a favorite
     */
    public FavoriteEntity(UserEntity userEntity, GameEntity gameEntity) {
        this.userEntity = userEntity;
        this.gameEntity = gameEntity;
    }

    /**
     * Full constructor of the class
     * @param id of the favorite
     * @param userEntity of the favorite
     * @param gameEntity of the favorite
     */
    public FavoriteEntity(int id, UserEntity userEntity, GameEntity gameEntity) {
        this.id = id;
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
        FavoriteEntity favoriteEntity = (FavoriteEntity) o;
        return id == favoriteEntity.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "FavoriteEntity{" +
                "id=" + id +
                ", userEntity=" + userEntity +
                ", gameEntity=" + gameEntity +
                '}';
    }
}

