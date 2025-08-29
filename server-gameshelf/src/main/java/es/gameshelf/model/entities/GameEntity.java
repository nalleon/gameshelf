package es.gameshelf.model.entities;

import java.util.Objects;
import java.util.Set;
import jakarta.persistence.*;
import org.hibernate.annotations.Fetch;
import org.hibernate.annotations.FetchMode;

/**
 * @author Nabil L. A. @nalleon
 */
@Entity
@Table(name="games")
@NamedQuery(name="GameEntity.findAll", query="SELECT r FROM GameEntity r")
public class GameEntity {
    /**
     * Properties
     */
    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
    @Column(unique=true, nullable=false)
    private int id;

    @Column(unique = true, nullable=false, length=100, name = "title")
    private String title;

    @Column(length=20, name = "release_date")
    private String releaseDate;

    @Column(unique = true, nullable=false, length=100, name = "slug")
    private String slug;

    @Column(length=255, name = "cover")
    private String cover;

    @Column(name = "external_rating")
    private int externalRating;

    @ManyToMany(cascade = {CascadeType.PERSIST}, fetch = FetchType.EAGER)
    @Fetch(FetchMode.SELECT)
    @JoinTable(name = "games_developers",
            joinColumns = { @JoinColumn(name = "game_id") },
            inverseJoinColumns = { @JoinColumn(name = "developers_id")})
    private Set<DeveloperEntity> developerEntitySet;

    private Set<PublisherEntity> publisherEntitySet;
    private Set<FormatEntity> formatEntitySet;
    private Set<PlatformEntity> platformEntitySet;
    private Set<GenreEntity> genreEntitySet;

    /**
     * Default constructor of the class
     */
    public GameEntity() {}

    /**
     * Constructor of the class
     * @param id of the game
     */
    public GameEntity(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param title of the game
     */
    public GameEntity(String title) {
        this.title = title;
    }

    /**
     * Full constructor of the class
     * @param title of the game
     * @param releaseDate of the game
     * @param slug of the game
     * @param cover of the game
     * @param externalRating of the game
     * @param developerEntitySet of the game
     * @param publisherEntitySet of the game
     * @param formatEntitySet of the game
     * @param platformEntitySet of the game
     * @param genreEntitySet of the game
     */
    public GameEntity(String title, String releaseDate, String slug, String cover, int externalRating,
                      Set<DeveloperEntity> developerEntitySet, Set<PublisherEntity> publisherEntitySet, Set<FormatEntity> formatEntitySet,
                      Set<PlatformEntity> platformEntitySet, Set<GenreEntity> genreEntitySet) {
        this.title = title;
        this.releaseDate = releaseDate;
        this.slug = slug;
        this.cover = cover;
        this.externalRating = externalRating;
        this.developerEntitySet = developerEntitySet;
        this.publisherEntitySet = publisherEntitySet;
        this.formatEntitySet = formatEntitySet;
        this.platformEntitySet = platformEntitySet;
        this.genreEntitySet = genreEntitySet;
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

    public Set<DeveloperEntity> getDeveloperSet() {
        return developerEntitySet;
    }

    public void setDeveloperSet(Set<DeveloperEntity> developerEntitySet) {
        this.developerEntitySet = developerEntitySet;
    }

    public Set<PublisherEntity> getPublisherSet() {
        return publisherEntitySet;
    }

    public void setPublisherSet(Set<PublisherEntity> publisherEntitySet) {
        this.publisherEntitySet = publisherEntitySet;
    }

    public Set<FormatEntity> getFormatSet() {
        return formatEntitySet;
    }

    public void setFormatSet(Set<FormatEntity> formatEntitySet) {
        this.formatEntitySet = formatEntitySet;
    }

    public Set<PlatformEntity> getPlatformSet() {
        return platformEntitySet;
    }

    public void setPlatformSet(Set<PlatformEntity> platformEntitySet) {
        this.platformEntitySet = platformEntitySet;
    }

    public Set<GenreEntity> getGenreSet() {
        return genreEntitySet;
    }

    public void setGenreSet(Set<GenreEntity> genreEntitySet) {
        this.genreEntitySet = genreEntitySet;
    }

    @Override
    public String toString() {
        return "GameEntity{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", releaseDate='" + releaseDate + '\'' +
                ", slug='" + slug + '\'' +
                ", cover='" + cover + '\'' +
                ", externalRating=" + externalRating +
                ", developerEntitySet=" + developerEntitySet +
                ", publisherEntitySet=" + publisherEntitySet +
                ", formatEntitySet=" + formatEntitySet +
                ", platformEntitySet=" + platformEntitySet +
                ", genreEntitySet=" + genreEntitySet +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        GameEntity gameEntity = (GameEntity) o;
        return id == gameEntity.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }
}
