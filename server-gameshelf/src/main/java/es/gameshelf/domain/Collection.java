package es.gameshelf.domain;

import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class Collection {

    /**
     * Properties
     */
    private int id;
    private User user;

    /**
     * Default constructor of the class
     */
    public Collection() {}

    /**
     * Constructor of the class
     * @param user of the collection
     * @implNote for creating a collection
     */
    public Collection(User user) {
        this.user = user;
    }

    /**
     * Full constructor of the class
     * @param id of the collection
     * @param user of the collection
     */
    public Collection(int id, User user) {
        this.id = id;
        this.user = user;
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


    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Collection collection = (Collection) o;
        return id == collection.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "Collection{" +
                "id=" + id +
                ", user=" + user +
                '}';
    }
}

