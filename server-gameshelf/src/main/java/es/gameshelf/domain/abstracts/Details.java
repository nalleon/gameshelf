package es.gameshelf.domain.abstracts;

import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public abstract class Details {
    /**
     * Properties
     */
    private int id;
    private String name;
    private String additionalText;

    /**
     * Default constructor of the class
     */
    public Details() {}

    /**
     * Constructor of the class
     * @param id of the detail
     */
    public Details(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param name of the detail
     */
    public Details(String name) {
        this.name = name;
    }

    /**
     * Constructor of the class
     * @param name of the detail
     * @param additionalText of the detail
     */
    public Details(String name, String additionalText) {
        this.name = name;
        this.additionalText = additionalText;
    }

    /**
     * Full constructor of the class
     * @param id of the detail
     * @param name of the detail
     * @param additionalText of the detail
     */
    public Details(int id, String name, String additionalText) {
        this.id = id;
        this.name = name;
        this.additionalText = additionalText;
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

    public String getAdditionalText() {
        return additionalText;
    }

    public void setAdditionalText(String additionalText) {
        this.additionalText = additionalText;
    }

    /**
     * Equals and hashcode
     */
    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Details that = (Details) o;
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
                ", additionalText='" + additionalText + '\'' +
                '}';
    }
}
