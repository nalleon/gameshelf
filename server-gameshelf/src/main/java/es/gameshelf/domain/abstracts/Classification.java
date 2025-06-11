package es.gameshelf.domain.abstracts;

import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public abstract class Classification {
    /**
     * Properties
     */
    private int id;
    private String name;

    /**
     * Default constructor of the class
     */
    public Classification() {}

    /**
     * Constructor of the class
     * @param id of the classification
     */
    public Classification(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param name of the classification
     */
    public Classification(String name) {
        this.name = name;
    }

    /**
     * Full constructor of the class
     * @param id of the classification
     * @param name of the classification
     */
    public Classification(int id, String name) {
        this.id = id;
        this.name = name;
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

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    /**
     * Equals and hashcode
     */
    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Classification that = (Classification) o;
        return Objects.equals(name, that.name);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(name);
    }

    @Override
    public String toString() {
        return getClass().getSimpleName()+"{" +
                "id=" + id +
                ", name='" + name + '\'' +
                '}';
    }
}
