package es.gameshelf.domain;

import java.util.Objects;
import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
public class Game {
    /**
     * Properties
     */
    private int id;
    private String title;
    private String releaseDate;
    private String slug;
    private String cover;
    private int externalRating;
    private Set<Developer> developerSet;
    private Set<Publisher> publisherSet;
    private Set<Format> formatSet;
    private Set<Platform> platformSet;
    private Set<Genre> genreSet;

    /**
     * Default constructor of the class
     */
    public Game() {}

    /**
     * Constructor of the class
     * @param id of the game
     */
    public Game(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param title of the game
     */
    public Game(String title) {
        this.title = title;
    }

    /**
     * Full constructor of the class
     * @param title of the game
     * @param releaseDate of the game
     * @param slug of the game
     * @param cover of the game
     * @param externalRating of the game
     * @param developerSet of the game
     * @param publisherSet of the game
     * @param formatSet of the game
     * @param platformSet of the game
     * @param genreSet of the game
     */
    public Game(String title, String releaseDate, String slug, String cover, int externalRating,
                Set<Developer> developerSet, Set<Publisher> publisherSet, Set<Format> formatSet,
                Set<Platform> platformSet, Set<Genre> genreSet) {
        this.title = title;
        this.releaseDate = releaseDate;
        this.slug = slug;
        this.cover = cover;
        this.externalRating = externalRating;
        this.developerSet = developerSet;
        this.publisherSet = publisherSet;
        this.formatSet = formatSet;
        this.platformSet = platformSet;
        this.genreSet = genreSet;
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

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getReleaseDate() {
        return releaseDate;
    }

    public void setReleaseDate(String releaseDate) {
        this.releaseDate = releaseDate;
    }

    public String getSlug() {
        return slug;
    }

    public void setSlug(String slug) {
        this.slug = slug;
    }

    public String getCover() {
        return cover;
    }

    public void setCover(String cover) {
        this.cover = cover;
    }

    public int getExternalRating() {
        return externalRating;
    }

    public void setExternalRating(int externalRating) {
        this.externalRating = externalRating;
    }

    public Set<Developer> getDeveloperSet() {
        return developerSet;
    }

    public void setDeveloperSet(Set<Developer> developerSet) {
        this.developerSet = developerSet;
    }

    public Set<Publisher> getPublisherSet() {
        return publisherSet;
    }

    public void setPublisherSet(Set<Publisher> publisherSet) {
        this.publisherSet = publisherSet;
    }

    public Set<Format> getFormatSet() {
        return formatSet;
    }

    public void setFormatSet(Set<Format> formatSet) {
        this.formatSet = formatSet;
    }

    public Set<Platform> getPlatformSet() {
        return platformSet;
    }

    public void setPlatformSet(Set<Platform> platformSet) {
        this.platformSet = platformSet;
    }

    public Set<Genre> getGenreSet() {
        return genreSet;
    }

    public void setGenreSet(Set<Genre> genreSet) {
        this.genreSet = genreSet;
    }

    @Override
    public String toString() {
        return "Game{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", releaseDate='" + releaseDate + '\'' +
                ", slug='" + slug + '\'' +
                ", cover='" + cover + '\'' +
                ", externalRating=" + externalRating +
                ", developerSet=" + developerSet +
                ", publisherSet=" + publisherSet +
                ", formatSet=" + formatSet +
                ", platformSet=" + platformSet +
                ", genreSet=" + genreSet +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Game game = (Game) o;
        return id == game.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }
}
