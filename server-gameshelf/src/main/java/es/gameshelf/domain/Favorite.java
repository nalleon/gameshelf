package es.gameshelf.domain;

import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class Favorite {

    /**
     * Properties
     */
    private int id;
    private User user;
    private Game game;

    /**
     * Default constructor of the class
     */
    public Favorite() {}

    /**
     * Constructor of the class
     * @param user of the favorite
     * @param game of the favorite
     * @implNote for creating a favorite
     */
    public Favorite(User user, Game game) {
        this.user = user;
        this.game = game;
    }

    /**
     * Full constructor of the class
     * @param id of the favorite
     * @param user of the favorite
     * @param game of the favorite
     */
    public Favorite(int id, User user, Game game) {
        this.id = id;
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
        Favorite favorite = (Favorite) o;
        return id == favorite.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "Favorite{" +
                "id=" + id +
                ", user=" + user +
                ", game=" + game +
                '}';
    }
}

